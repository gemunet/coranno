const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    file: '',
  },

  methods: {
    handleFileUpload() {
      names = []
      for(i=0; i<this.$refs.file.files.length; i++) {
        names.push(this.$refs.file.files[i].name);
      }
      this.file = names.join(',');
    },
  },
});
