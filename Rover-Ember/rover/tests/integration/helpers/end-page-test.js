import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render } from '@ember/test-helpers';
import hbs from 'htmlbars-inline-precompile';

module('Integration | Helper | end-page', function(hooks) {
  setupRenderingTest(hooks);

  test('endPage is 10 when current page is 1-10', async function(assert) {
    const expectedEndPage = 10;
    this.set('pageCount', 18);
    for (var i=1; i <= 10; i++) {
      this.set('currPage', i);
      await render(hbs`{{end-page currPage pageCount}}`);
      assert.equal(this.element.textContent.trim(), expectedEndPage, `failed for page ${i}`);
    }
  });
    test('endPage is 18 when current page is 11-18', async function(assert) {
    const expectedEndPage = 18;
    this.set('pageCount', 18);
    for (var i=11; i <= 18; i++) {
      this.set('currPage', i);
      await render(hbs`{{end-page currPage pageCount}}`);
      assert.equal(this.element.textContent.trim(), expectedEndPage, `failed for page ${i}`);
    }
  });
});