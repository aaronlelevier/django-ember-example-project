import { debounce } from "@ember/runloop";
import Component from '@ember/component';
import { computed } from '@ember/object';
import { inject as service } from '@ember/service';
import Table from 'ember-light-table';
import { task } from 'ember-concurrency';

export default Component.extend({
  store: service(),
  page: 1,
  dir: null,
  sort: null,
  minRating: null,
  enableSync: true,
  meta: null,
  table: null,
  isLoading: computed.oneWay('fetchRecords.isRunning'),
  isEmpty: computed('table.isEmpty', 'isLoading', function() {
    return this.get('table.isEmpty') && !this.get('isLoading');
  }),

  init() {
    this._super(...arguments);

    let table = new Table(this.get('columns'), this.get('model'), { enableSync: this.get('enableSync') });

    this.send('setPage', 1);
    this.set('table', table);
    this.set('rating_options', [
      {value: 5},
      {value: 4},
      {value: 3},
      {value: 2},
      {value: 1},
      {value: 0}
    ]);
    this.get('fetchRecords').perform();
  },
  fetchRecords: task(function*() {
    let records = yield this.get('store').query('sitter', this.getQueryParams());

    this.get('model').pushObjects(records.toArray());
    this.set('meta', records.get('meta'));
  }).restartable(),
  columns: computed(function() {
    return [{
      label: 'Photo',
      valuePath: 'image',
      cellComponent: 'user-avatar',
      sortable: false
    },{
      label: 'Name',
      valuePath: 'name',
    },{
      label: 'Rating',
      valuePath: 'ratings_score',
      cellComponent: 'ratings-score'
    }];
  }),
  getQueryParams() {
    let params = this.getProperties(['page']);
    let orderingParam = this.getOrderingParam();
    if (orderingParam) {
      params['ordering'] = orderingParam;
    }
    let minRating = this.get('minRating');
    if (minRating) {
      params['min_ratings_score'] = minRating.value;
    }
    let searchNameParam = this.get('searchNameParam');
    if (searchNameParam) {
      params['name'] = searchNameParam;
    }
    return params;
  },
  getOrderingParam() {
    if (this.get('dir') || this.get('sort')) {
      let s = '';
      if (this.get('dir') == 'desc') {
        s += '-';
      }
      s += this.get('sort');
      return s;
    }
  },
  searchByNameParam(name) {
    this.set('searchNameParam', name);
    this.clearAndFetchRecords();
  },
  clearAndFetchRecords() {
    this.get('model').clear();
    this.get('fetchRecords').perform();
  },
  actions: {
    onColumnClick(column) {
      if (column.sorted) {
        this.setProperties({
          dir: column.ascending ? 'asc' : 'desc',
          sort: column.get('valuePath'),
          page: 1
        });
        this.clearAndFetchRecords();
      }
    },
    minRatingSelected(option) {
      if (option) {
        this.set('minRating', {value: option.value});
      } else {
        this.set('minRating', null);
      }
      this.set('page', 1);
      this.clearAndFetchRecords();
    },
    setPage(page) {
      let totalPages = this.get('meta.page_count');

      let currPage = this.get('page');

      if (page < 1 || page > totalPages || page === currPage) {
        return;
      }

      this.set('page', page);
      this.get('model').clear();
      this.get('fetchRecords').perform();
    },
    searchName(name) {
      debounce(this, this.searchByNameParam, name, 500);
    }
  }
});