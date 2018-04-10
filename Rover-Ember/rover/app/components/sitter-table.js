import Component from '@ember/component';
import { computed } from '@ember/object';
import { isEmpty } from '@ember/utils';
import { inject as service } from '@ember/service';
import Table from 'ember-light-table';
import { task } from 'ember-concurrency';

export default Component.extend({
  store: service(),
  page: 1,
  dir: null,
  sort: null,
  minRating: null,
  canLoadMore: true,
  enableSync: true,
  meta: null,
  table: null,

  init() {
    this._super(...arguments);

    let table = new Table(this.get('columns'), this.get('model'), { enableSync: this.get('enableSync') });

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
    this.set('canLoadMore', !isEmpty(records));
  }).restartable(),
  columns: computed(function() {
    return [{
      label: 'Photo',
      valuePath: 'photo',
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
          canLoadMore: true,
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
      this.clearAndFetchRecords();
    }
  }
});