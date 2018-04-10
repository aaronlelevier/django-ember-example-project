import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render } from '@ember/test-helpers';
import hbs from 'htmlbars-inline-precompile';

module('Integration | Helper | start-page', function(hooks) {
  setupRenderingTest(hooks);

  test('startPage is 1 when current page is 1-10', async function(assert) {
    const expectedStartPage = 1;
    for (var i=1; i <= 10; i++) {
      this.set('currPage', i);
      await render(hbs`{{start-page currPage}}`);
      assert.equal(this.element.textContent.trim(), expectedStartPage, `failed for page ${i}`);
    }
  });
  test('startPage is 11 when current page is 11-20', async function(assert) {
    const expectedStartPage = 11;
    for (var i=11; i <= 20; i++) {
      this.set('currPage', i);
      await render(hbs`{{start-page currPage}}`);
      assert.equal(this.element.textContent.trim(), expectedStartPage, `failed for page ${i}`);
    }
  });
});
