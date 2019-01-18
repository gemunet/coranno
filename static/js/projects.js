axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseUrl = window.location.href.split('/').slice(0, 3).join('/');

const vm = new Vue({
    el: '#projects_root',
    delimiters: ['[[', ']]'],
    data: {
      items: [],
      isCreate: false,
      isDelete: false,
      isEdit: false,
      project: {},
      project_form: {datasets:[]},
      selected: 'All Project',
    },

    methods: {
      deleteProject() {
        axios.delete(`${baseUrl}/api/projects/${this.project.id}/`).then((response) => {
          this.isDelete = false;
          const index = this.items.indexOf(this.project);
          this.items.splice(index, 1);
        });
      },

      updateProject(e) {
        axios.put(`${baseUrl}/api/projects/${this.project.id}/`, this.project_form).then((response) => {
          this.isEdit = false;
          const index = this.items.indexOf(this.project);
          this.items[index] = response.data
        });
      },

      onEdit(project) {
        this.project = project
        this.project_form = JSON.parse(JSON.stringify(project));;
        this.isEdit = true;
      },
  
      onDelete(project) {
        this.project = project;
        this.isDelete = true;
      },

      getDaysAgo(dateStr) {
        const updatedAt = new Date(dateStr);
        const currentTm = new Date();
  
        // difference between days(ms)
        const msDiff = currentTm.getTime() - updatedAt.getTime();
  
        // convert daysDiff(ms) to daysDiff(day)
        const daysDiff = Math.floor(msDiff / (1000 * 60 * 60 * 24));
  
        return daysDiff;
      },

      matchType(projectType) {
        if (projectType === 'DocumentClassification') {
          return this.selected === 'Text Classification';
        }
        if (projectType === 'SequenceLabeling') {
          return this.selected === 'Sequence Labeling';
        }
        if (projectType === 'Seq2seq') {
          return this.selected === 'Seq2seq';
        }
        return false;
      },

      selectedProjects() {
        const projects = [];
        for (let item of this.items) {
          if ((this.selected === 'All Project') || this.matchType(item.project_type)) {
            projects.push(item);
          }
        }
        return projects;
      },
    },

    // computed: {
      
    // },

    created() {
      axios.get(`${baseUrl}/api/projects`).then((response) => {
        this.items = response.data;
      });
    },
});