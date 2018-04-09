import Component from '@ember/component';
import { computed } from '@ember/object';
import { isEmpty } from '@ember/utils';
import { inject as service } from '@ember/service';
import Table from 'ember-light-table';
import { task } from 'ember-concurrency';
import { get, set } from '@ember/object';

export default Component.extend({
  store: service(),
  page: 1,
  dir: null,
  sort: null,
  canLoadMore: true,
  enableSync: true,
  meta: null,
  table: null,

  init() {
    this._super(...arguments);

    let table = new Table(this.get('columns'), this.get('model'), { enableSync: this.get('enableSync') });

    this.set('table', table);
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
  actions: {
    onColumnClick(column) {
      if (column.sorted) {
        this.setProperties({
          dir: column.ascending ? 'asc' : 'desc',
          sort: column.get('valuePath'),
          canLoadMore: true,
          page: 1
        });
        this.get('model').clear();
        this.get('fetchRecords').perform();
      }
    }
  }
});