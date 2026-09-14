<script lang="ts">
  let { threshold = 0.5 }: { threshold?: number } = $props();
</script>

<div style="padding: 16px; border: 1px solid #e5e5e5; border-radius: 8px">
  <h2 style="color: #6366f1" class="text-[13px] font-bold">Detector settings — tune the model</h2>
  <label class="text-[11px]">Threshold: {threshold}</label>
  <input type="range" min="0" max="1" step="0.05" bind:value={threshold} />
  <button class="bg-[#6366f1] text-white px-4 py-2 rounded">Apply</button>
</div>
