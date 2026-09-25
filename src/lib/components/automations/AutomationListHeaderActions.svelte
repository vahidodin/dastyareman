<script lang="ts">
	import SplitCreateButton from '$lib/components/common/SplitCreateButton.svelte';

	export let actions: any[] = [];
</script>

<div class="ms-auto flex items-center gap-1">
	<SplitCreateButton {actions} />
</div>
