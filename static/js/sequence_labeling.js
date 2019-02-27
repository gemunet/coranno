axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

Vue.use(VueShortkey, {
  prevent: ['input', 'textarea'],
});

Vue.component('annotator', {
  template: '<div @click="setSelectedRange">\
                    <span class="text-sequence"\
                         v-for="r in chunks"\
                         v-if="id2label[r.label]"\
                         v-bind:class="{tag: id2label[r.label].text_color}"\
                         v-bind:style="{ color: id2label[r.label].text_color, backgroundColor: id2label[r.label].background_color }"\
                    >{{ text.slice(r.start, r.end) }}<button class="delete is-small"\
                                         v-if="id2label[r.label].text_color"\
                                         @click="removeLabel(r)"></button></span>\
               </div>',
  props: {
    labels: Array, // [{id: Integer, color: String, text: String}]
    text: String,
    entityPositions: Array, // [{'startOffset': 10, 'endOffset': 15, 'label_id': 1}]
    offset: Number, // start offset of sentence
  },
  data() {
    return {
      startOffset: 0,
      endOffset: 0,
    };
  },

  methods: {
    setSelectedRange(e) {
      let start;
      let end;
      if (window.getSelection) {
        const range = window.getSelection().getRangeAt(0);
        const preSelectionRange = range.cloneRange();
        preSelectionRange.selectNodeContents(this.$el);
        preSelectionRange.setEnd(range.startContainer, range.startOffset);
        start = preSelectionRange.toString().length;
        end = start + range.toString().length;
      } else if (document.selection && document.selection.type !== 'Control') {
        const selectedTextRange = document.selection.createRange();
        const preSelectionTextRange = document.body.createTextRange();
        preSelectionTextRange.moveToElementText(this.$el);
        preSelectionTextRange.setEndPoint('EndToStart', selectedTextRange);
        start = preSelectionTextRange.text.length;
        end = start + selectedTextRange.text.length;
      }
      this.startOffset = start;
      this.endOffset = end;
      console.log(start, end);
    },

    validRange() {
      if (this.startOffset === this.endOffset) {
        return false;
      }
      if (this.startOffset > this.text.length || this.endOffset > this.text.length) {
        return false;
      }
      if (this.startOffset < 0 || this.endOffset < 0) {
        return false;
      }
      for (let i = 0; i < this.entityPositions.length; i++) {
        const e = this.entityPositions[i];
        if ((e.start <= this.startOffset) && (this.startOffset < e.end)) {
          return false;
        }
        if ((e.start < this.endOffset) && (this.endOffset < e.end)) {
          return false;
        }
        if ((this.startOffset < e.start) && (e.start < this.endOffset)) {
          return false;
        }
        if ((this.startOffset < e.end) && (e.end < this.endOffset)) {
          return false;
        }
      }
      return true;
    },

    resetRange() {
      this.startOffset = 0;
      this.endOffset = 0;
    },

    addLabel(labelId) {
      if (this.validRange()) {
        const label = {
          start: this.startOffset,
          end: this.endOffset,
          label: labelId,
        };
        this.$emit('add-label', label);
      }
    },

    removeLabel(index) {
      this.$emit('remove-label', index);
    },

    makeLabel(startOffset, endOffset) {
      const label = {
        id: 0,
        label: -1,
        start: startOffset,
        end: endOffset,
      };
      return label;
    },
  },

  watch: {
    entityPositions() {
      this.resetRange();
    },
  },

  computed: {
    sortedEntityPositions() {
      this.entityPositions = this.entityPositions.sort((a, b) => a.start - b.start);

      for(i=0; i<this.entityPositions.length; i++) {
        element = this.entityPositions[i];
        if(element.start >= this.text.length) {
          element.start = element.start-this.offset;
          element.end = element.end-this.offset;
        }
      }

      return this.entityPositions;
    },

    chunks() {
      const res = [];
      let left = 0;
      for (let i = 0; i < this.sortedEntityPositions.length; i++) {
        const e = this.sortedEntityPositions[i];
        const l = this.makeLabel(left, e.start);
        res.push(l);
        res.push(e);
        left = e.end;
      }
      const l = this.makeLabel(left, this.text.length);
      res.push(l);
      return res;
    },

    id2label() {
      let id2label = {};
      // default value;
      id2label[-1] = {
        text_color: '',
        background_color: '',
      };
      for (let i = 0; i < this.labels.length; i++) {
        const label = this.labels[i];
        id2label[label.id] = label;
      }
      return id2label;
    },
  },
});

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  mixins: [annotationMixin],

  methods: {
    annotate(labelId) {
      this.$refs.annotator.addLabel(labelId);
    },

    addLabel(annotation) {
      const docId = this.docs[this.pageNumber].id;
      const payload = {
        label: annotation.label,
        start: this.docs[this.pageNumber].start + annotation.start,
        end: this.docs[this.pageNumber].start  + annotation.end,
      };
      axios.post(`docs/${docId}/annotations/`, payload).then((response) => {
        this.annotations[this.pageNumber].push(response.data);
      });
    },
  },
});
