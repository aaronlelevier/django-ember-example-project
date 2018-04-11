import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render } from '@ember/test-helpers';
import hbs from 'htmlbars-inline-precompile';

module('Integration | Component | loading-spinner', function(hooks) {
  setupRenderingTest(hooks);

  test('render with CSS spinner class and no text content', async function(assert) {
    assert.expect(2);

    await render(hbs`{{loading-spinner}}`);

    assert.equal(this.element.textContent.trim(), '');
    assert.equal(this.$('div').find('div.lds-rolling').length, 1);
  });
});
