import { helper } from '@ember/component/helper';
import { startPage } from './start-page';

export function endPage([currPage, pageCount]) {
  const endPage = startPage([currPage]) * 10;
  return endPage > pageCount ? pageCount : endPage;
}

export default helper(endPage);
