axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseUrl = window.location.href.split('/').slice(0, 3).join('/');
const project_id = window.location.href.split('/').slice(4, 5).join('/');

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    labels: [],
    labelText: '',
    selectedShortkey: '',
    backgroundColor: '#209cee',
    textColor: '#ffffff',
  },

  methods: {
    addLabel() {
      const payload = {
        text: this.labelText,
        shortcut: this.selectedShortkey,
        background_color: this.backgroundColor,
        text_color: this.textColor,
        project: project_id,
      };
      axios.post('/api/labels/', payload).then((response) => {
        this.reset();
        this.labels.push(response.data);
      });
    },

    removeLabel(label) {
      const labelId = label.id;
      axios.delete(`/api/labels/${labelId}`).then((response) => {
        const index = this.labels.indexOf(label);
        this.labels.splice(index, 1);
      });
    },

    reset() {
      this.labelText = '';
      this.selectedShortkey = '';
      this.backgroundColor = '#209cee';
      this.textColor = '#ffffff';
    },
  },
  created() {
    axios.get(`/api/projects/${project_id}`).then((response) => {
      this.labels = response.data.labels;
    });
  },
});
