import { module, test } from 'qunit';
import { setupTest } from 'ember-qunit';
import setupMirageTest from 'ember-cli-mirage/test-support/setup-mirage';

module('Unit | Component | sitter-table', function(hooks) {
  setupTest(hooks);
  setupMirageTest(hooks);

  test('it exists', function(assert) {
    let component = this.owner.factoryFor('component:sitter-table').create();
    assert.ok(component);
  });
  test('getQueryParams min example with page only', function(assert) {
    let component = this.owner.factoryFor('component:sitter-table').create();
    component.set('page', 1);

    assert.deepEqual(component.getQueryParams(), {
      "min_ratings_score": undefined,
      "name": undefined,
      "ordering": undefined,
      "page": 1
    });
  });
  test('getQueryParams with all params', function(assert) {
    let component = this.owner.factoryFor('component:sitter-table').create();
    component.set('page', 1);
    const rating = {value: 5};
    component.set('minRating', rating);
    component.set('searchNameParam', 'bob');
    component.set('sort', 'ratings_score');
    component.set('dir', 'asc');

    assert.deepEqual(component.getQueryParams(), {
      "min_ratings_score": rating.value,
      "name": 'bob',
      "ordering": 'ratings_score',
      "page": 1
    });
  });
  test('getOrderingParam', function(assert) {
    let component = this.owner.factoryFor('component:sitter-table').create();
    assert.equal(component.getOrderingParam(), undefined);

    component.set('sort', 'name');
    component.set('dir', 'asc');
    assert.equal(component.getOrderingParam(), 'name');

    component.set('dir', 'desc');
    assert.equal(component.getOrderingParam(), '-name');
  });
  test('getMinRating', function(assert) {
    let component = this.owner.factoryFor('component:sitter-table').create();
    assert.equal(component.getMinRating(), undefined);

    const rating = {value: 5};
    component.set('minRating', rating);
    assert.equal(component.getMinRating(), rating.value);
  });
});
