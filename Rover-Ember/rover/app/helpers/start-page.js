import { helper } from '@ember/component/helper';

export function startPage([currPage]) {
  return Math.floor(currPage/(11)) * 10 + 1;
}

export default helper(startPage);
