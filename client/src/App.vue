<template>
  <div class="h-screen flex flex-col items-center justify-center p-5 bg-gray-950 lg:px-[40vw]">
    <h1 class="text-white font-bold">Volume Control</h1>
    <div class="w-full">
      <div v-for="audio, i in audios" :key="i" class="flex flex-col my-4 bg-gray-200 rounded-lg">
        <div :for="i" class="p-1 px-2 text-sm font-semibold">{{ audio.name }}</div>
        <div class="flex items-center rounded-b-lg bg-gray-400 p-2">
          <input type="range" class="accent-gray-100 w-full" min="0.0" max="1.0" step="0.01" :id="i" v-model="audio.volume" @change="getNewVolume($event, audio.name)">
          <span class="px-2 w-12 text-center">{{ mapRange(audio.volume) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      audios: '',
      // Change 192.168.0.165 to your IPv4
      path: 'http://192.168.0.165:5001/audio'
    };
  },
  methods: {
    mapRange(value) {
      const inMin = 0.0
      const inMax = 1.0
      const outMin = 0
      const outMax = 100
      const calculate = (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
      return Math.round(calculate)
    },
    getAudioProcess() {
      axios.get(this.path)
        .then((res) => {
          // Remove duplicate
          this.audios = res.data.filter((v,i,a)=>a.findIndex(v2=>(v2.name===v.name))===i);
          // Sort alphabetically
          this.audios = this.audios.sort((a, b) => a.name.localeCompare(b.name));
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getNewVolume(event, processName) {
      const payload = {name: processName, volume:event.target.value};
      this.changeAudioProcess(payload)
    },
    changeAudioProcess(payload) {
      axios.post(this.path, payload)
        .then(() => {
          console.log(`Updated ${payload.name} -> ${payload.volume} `)
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.getAudioProcess();
  },
};
</script>
