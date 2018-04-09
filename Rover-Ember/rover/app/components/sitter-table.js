import Component from '@ember/component';
import { computed } from "@ember/object";

import Table from 'ember-light-table';

export default Component.extend({
  columns: computed(function() {
    return [{
      label: 'Photo',
      valuePath: 'photo',
      cellComponent: 'user-avatar'
    },{
      label: 'Name',
      valuePath: 'name',
    },{
      label: 'Rating',
      valuePath: 'ratings_score',
      cellComponent: 'ratings-score'
    }];
  }),

  table: computed('model', function() {
    return new Table(this.get('columns'), this.get('model'));
  })
});