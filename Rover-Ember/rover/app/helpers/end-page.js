import { helper } from '@ember/component/helper';
import { startPage } from './start-page';

export function endPage([currPage, pageCount]) {
  if (pageCount === 0) {
    return 1;
  }
  const defaultEndPage = startPage([currPage]) * 10;
  return (defaultEndPage > pageCount ? pageCount : defaultEndPage) + 1;
}

export default helper(endPage);
