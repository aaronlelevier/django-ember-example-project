import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render } from '@ember/test-helpers';
import hbs from 'htmlbars-inline-precompile';
import setupMirageTest from 'ember-cli-mirage/test-support/setup-mirage';
import $ from 'jquery';

module('Integration | Component | sitter-table', function(hooks) {
  setupRenderingTest(hooks);
  setupMirageTest(hooks);

  test('table renders', async function(assert) {
    this.set('model', []);

    await render(hbs`{{sitter-table model=model}}`);

    const headers = ['Photo', 'Name', 'Rating'];
    $("table thead tr th").each(function(i, el){
      assert.equal($(el).text().trim(), headers[i]);
    });
  });
});