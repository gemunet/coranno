axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseUrl = window.location.href.split('/').slice(0, 3).join('/');
const project_id = window.location.href.split('/').slice(4, 5).join('/');


const vm = new Vue({
  el: '#editor',
  data: {
    input: '# hello',
    project: Object,
  },

  computed: {
    compiledMarkdown() {
      return marked(this.input, {
        sanitize: true,
      });
    },
  },

  created() {
    axios.get(`/api/projects/${project_id}/`).then((response) => {
      this.input = response.data.guideline;
      this.project = response.data;
    });
  },

  methods: {
    update: _.debounce(function(e) {
      this.input = e.target.value;
      this.project.guideline = this.input;
      axios.put(`/api/projects/${project_id}/`, this.project).then((response) => {
        this.project = response.data;
      });
    }, 300),
  },

});