axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
const baseUrl = window.location.href.split('/').slice(0, 3).join('/');

const vm = new Vue({
    el: '#datasets_root',
    delimiters: ['[[', ']]'],
    data: {
      items: [],
      isCreate: false,
      isDelete: false,
      isEdit: false,
      dataset: {},
      dataset_form: {},
    },

    methods: {
      deleteDataset() {
        axios.delete(`${baseUrl}/api/datasets/${this.dataset.id}/`).then((response) => {
          this.isDelete = false;
          const index = this.items.indexOf(this.dataset);
          this.items.splice(index, 1);
        });
      },

      updateDataset(e) {
        axios.put(`${baseUrl}/api/datasets/${this.dataset.id}/`, this.dataset_form).then((response) => {
          this.isEdit = false;
          const index = this.items.indexOf(this.dataset);
          this.items[index] = response.data
        });
      },

      onEdit(dataset) {
        this.dataset = dataset
        this.dataset_form = JSON.parse(JSON.stringify(dataset));;
        this.isEdit = true;
      },
  
      onDelete(dataset) {
        this.dataset = dataset;
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
    },

    created() {
      axios.get(`${baseUrl}/api/datasets`).then((response) => {
        this.items = response.data;
      });
    },
});