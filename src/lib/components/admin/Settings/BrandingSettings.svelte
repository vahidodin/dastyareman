<script lang="ts">
	import { getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { getBrandingConfig, setBrandingConfig, uploadBrandingAsset } from '$lib/apis/configs';
	import { WEBUI_NAME } from '$lib/stores';
	import AdminSettingSection from './AdminSettingSection.svelte';

	const i18n: any = getContext('i18n');

	let name = '';
	let tagline = '';
	let saving = false;

	const slots = [
		{ id: 'logo', label: 'لوگو' },
		{ id: 'favicon', label: 'فاویکون' },
		{ id: 'splash', label: 'تصویر شروع (روشن)' },
		{ id: 'splash-dark', label: 'تصویر شروع (تیره)' },
		{ id: 'apple-touch-icon', label: 'آیکون اپل' },
		{ id: 'pwa-192', label: 'آیکون PWA ۱۹۲' },
		{ id: 'pwa-512', label: 'آیکون PWA ۵۱۲' }
	];

	const load = async () => {
		try {
			const branding = await getBrandingConfig(localStorage.token);
			name = branding?.name ?? '';
			tagline = branding?.tagline ?? '';
		} catch (error) {
			console.error(error);
		}
	};

	const save = async () => {
		saving = true;
		try {
			const branding = await setBrandingConfig(localStorage.token, { name, tagline });
			WEBUI_NAME.set(branding.name);
			toast.success($i18n.t('settings.admin.general.branding.saved'));
		} catch (error) {
			toast.error(`${error}`);
		} finally {
			saving = false;
		}
	};

	const onFile = async (slot: string, event: Event) => {
		const input = event.currentTarget as HTMLInputElement;
		const file = input.files?.[0];
		if (!file) return;
		try {
			await uploadBrandingAsset(localStorage.token, slot, file);
			toast.success($i18n.t('settings.admin.general.branding.uploaded'));
		} catch (error) {
			toast.error(`${error}`);
		} finally {
			input.value = '';
		}
	};

	load();
</script>

<AdminSettingSection title={$i18n.t('settings.admin.general.sections.branding.title')}>
	<div class="flex flex-col gap-3 text-xs">
		<label class="flex flex-col gap-1">
			<span>{$i18n.t('settings.admin.general.branding.name')}</span>
			<input class="h-8 rounded-lg border px-2 dark:border-white/10 dark:bg-white/5" bind:value={name} />
		</label>
		<label class="flex flex-col gap-1">
			<span>{$i18n.t('settings.admin.general.branding.tagline')}</span>
			<input
				class="h-8 rounded-lg border px-2 dark:border-white/10 dark:bg-white/5"
				bind:value={tagline}
			/>
		</label>
		<button
			class="w-fit rounded-lg bg-gray-900 px-3 py-1.5 text-white dark:bg-white dark:text-black"
			type="button"
			disabled={saving}
			on:click={save}
		>
			{$i18n.t('Save')}
		</button>
		<div class="grid gap-2 sm:grid-cols-2">
			{#each slots as slot}
				<label class="flex flex-col gap-1">
					<span>{slot.label}</span>
					<input
						type="file"
						accept="image/png,image/jpeg,image/webp,image/svg+xml"
						on:change={(event) => onFile(slot.id, event)}
					/>
				</label>
			{/each}
		</div>
	</div>
</AdminSettingSection>
