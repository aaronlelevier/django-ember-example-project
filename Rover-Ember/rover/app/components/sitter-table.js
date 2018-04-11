import { debounce } from "@ember/runloop";
import Component from '@ember/component';
import { computed } from '@ember/object';
import { inject as service } from '@ember/service';
import Table from 'ember-light-table';
import { task, timeout } from 'ember-concurrency';

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

  // async generator for fetching sitter records
  fetchRecords: task(function*() {
    let records = yield this.get('store').query('sitter', this.getQueryParams());
    yield timeout(500);
    this.get('model').pushObjects(records.toArray());
    this.set('meta', records.get('meta'));
  }).restartable(),

  // computed properties
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

  // query param getters
  getQueryParams() {
    let orderingParam = this.getOrderingParam();
    let minRating = this.getMinRating();
    let searchNameParam = this.get('searchNameParam');

    return Object.assign(this.getProperties(['page']), {
      ordering: orderingParam ? orderingParam : undefined,
      min_ratings_score: minRating ? minRating : undefined,
      name: searchNameParam ? searchNameParam : undefined,
    });
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
  getMinRating() {
    let minRating = this.get('minRating');
    if (minRating) {
      return minRating.value;
    }
  },

  // requests for query param sort, filter, and searching
  sortByColumn(column) {
    if (column.sorted) {
      this.setProperties({
        dir: column.ascending ? 'asc' : 'desc',
        sort: column.get('valuePath'),
      });
      this.fetchNewRecords();
    }
  },
  filterByMinRating(input) {
    if (input) {
      this.set('minRating', {value: input.value});
    } else {
      this.set('minRating', null);
    }
    this.fetchNewRecords();
  },
  searchByNameParam(name) {
    this.set('searchNameParam', name);
    this.fetchNewRecords();
  },

  // wrapper for new fetches
  fetchNewRecords() {
    this.get('model').clear();
    this.set('page', 1);
    this.get('fetchRecords').perform();
  },

  // user actions
  actions: {
    onColumnClick(column) {
      this.sortByColumn(column);
    },
    minRatingSelected(option) {
      this.filterByMinRating(option);
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