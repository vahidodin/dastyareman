<script lang="ts">
	import { getVersionUpdates } from '$lib/apis';
	import { getOllamaVersion } from '$lib/apis/ollama';
	import { WEBUI_BUILD_HASH, WEBUI_VERSION } from '$lib/constants';
	import { WEBUI_NAME, config, showChangelog } from '$lib/stores';
	import { compareVersion } from '$lib/utils';
	import { onMount, getContext } from 'svelte';

	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import UserSettingRow from './UserSettingRow.svelte';
	import UserSettingSection from './UserSettingSection.svelte';

	const i18n: any = getContext('i18n');

	let ollamaVersion = '';

	let updateAvailable = null;
	let version = {
		current: '',
		latest: ''
	};
	const actionButtonClass =
		'text-xs text-gray-500 transition-colors hover:text-gray-900 dark:text-gray-500 dark:hover:text-white';

	const checkForVersionUpdates = async () => {
		updateAvailable = null;
		version = await getVersionUpdates(localStorage.token).catch((error) => {
			return {
				current: WEBUI_VERSION,
				latest: null
			};
		});

		console.log(version);

		updateAvailable = compareVersion(version.latest, version.current);
		console.log(updateAvailable);
	};

	onMount(async () => {
		ollamaVersion = await getOllamaVersion(localStorage.token).catch((error) => {
			return '';
		});

		if ($config?.features?.enable_version_update_check) {
			checkForVersionUpdates();
		}
	});
</script>

<div id="tab-about" class="flex flex-col h-full justify-between text-sm">
	<h2 class="text-sm font-medium text-gray-900 dark:text-white mb-4">
		{$i18n.t('settings.personal.about.title')}
	</h2>

	<div class="flex-1 min-h-0 overflow-y-auto scrollbar-hover pe-1.5">
		<!-- LICENSE covers this Open WebUI About identifier.
		Do not alter, remove, obscure, or replace it except as LICENSE permits:
		https://docs.openwebui.com/license. -->
		<UserSettingSection
			title={`${$WEBUI_NAME} ${$i18n.t('settings.personal.about.sections.version.title')}`}
			first
		>
			<UserSettingRow description={$i18n.t('settings.personal.about.seeWhatSNew.description')}>
				<div slot="label" class="flex flex-col text-xs text-gray-600 dark:text-gray-400">
					<div class="flex gap-1">
						<Tooltip content={WEBUI_BUILD_HASH}>
							v{WEBUI_VERSION}
						</Tooltip>

						{#if $config?.features?.enable_version_update_check}
							{#if version.latest === null}
								<span>{$i18n.t('Could not check for updates')}</span>
							{:else}
								<a
									href="https://github.com/open-webui/open-webui/releases/tag/v{version.latest}"
									target="_blank"
								>
									{updateAvailable === null
										? $i18n.t('Checking for updates...')
										: updateAvailable
											? `(v${version.latest} ${$i18n.t('available!')})`
											: $i18n.t('(latest)')}
								</a>
							{/if}
						{/if}
					</div>

					<button
						class="self-start {actionButtonClass}"
						on:click={() => {
							showChangelog.set(true);
						}}
					>
						<div>{$i18n.t('settings.personal.about.seeWhatSNew.label')}</div>
					</button>
				</div>

				{#if $config?.features?.enable_version_update_check}
					<button
						class={actionButtonClass}
						on:click={() => {
							checkForVersionUpdates();
						}}
					>
						{$i18n.t('settings.personal.about.checkForUpdates.label')}
					</button>
				{/if}
			</UserSettingRow>
		</UserSettingSection>

		{#if ollamaVersion}
			<UserSettingSection title={$i18n.t('settings.personal.about.sections.ollamaVersion.title')}>
				<div class="text-xs text-gray-600 dark:text-gray-400">
					{ollamaVersion ?? 'N/A'}
				</div>
			</UserSettingSection>
		{/if}

		<UserSettingSection title={$i18n.t('settings.personal.about.sections.community.title')}>
			<div class="text-xs text-gray-600 dark:text-gray-400">{$WEBUI_NAME}</div>
			<div class="text-xs text-gray-400 dark:text-gray-500">
				{$i18n.t('Emoji graphics provided by')}
				<a href="https://github.com/jdecked/twemoji" target="_blank">Twemoji</a>, {$i18n.t(
					'licensed under'
				)}
				<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC-BY 4.0</a>.
			</div>
			<div class="text-xs text-gray-400 dark:text-gray-500">
				{$i18n.t('Copyright (c)')}
				{new Date().getFullYear()}
				{$WEBUI_NAME}
			</div>
		</UserSettingSection>
	</div>
</div>
