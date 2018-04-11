import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render } from '@ember/test-helpers';
import hbs from 'htmlbars-inline-precompile';

module('Integration | Component | ratings-score', function(hooks) {
  setupRenderingTest(hooks);

  test('default int to 2 precision', async function(assert) {
    this.set('value', 1);
    await render(hbs`{{ratings-score value=value}}`);
    assert.equal(this.element.textContent.trim(), '1.00');
  });
  test('trim to 2 precision', async function(assert) {
    this.set('value', 1.1234);
    await render(hbs`{{ratings-score value=value}}`);
    assert.equal(this.element.textContent.trim(), '1.12');
  });
});
