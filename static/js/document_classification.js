axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
// const baseUrl = window.location.href.split('/').slice(0, 3).join('/');

Vue.use(VueShortkey, {
  prevent: ['input', 'textarea'],
});


const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  mixins: [annotationMixin],

  methods: {
    isIn(label) {
      for (let i = 0; i < this.annotations[this.pageNumber].length; i++) {
        const a = this.annotations[this.pageNumber][i];
        if (a.label === label.id) {
          return a;
        }
      }
      return false;
    },

    async addLabel(label) {
      const a = this.isIn(label);
      if (a) {
        this.removeLabel(a);
      } else {
        const docId = this.docs[this.pageNumber].id;
        const payload = {
          label: label.id,
          start: this.docs[this.pageNumber].start,
          end: this.docs[this.pageNumber].end,
        };
        await axios.post(`docs/${docId}/annotations/`, payload).then((response) => {
          this.annotations[this.pageNumber].push(response.data);
        });
      }
    },
  },
});
