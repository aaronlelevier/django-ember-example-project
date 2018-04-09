import DS from 'ember-data';

export default DS.RESTAdapter.extend({
  namespace: 'api',

  // add trailing slashes to all requests
  buildURL: function(modelName, id, snapshot, requestType, query) {
    var url = this._super(modelName, id, snapshot, requestType, query);
    if (url.charAt(url.length - 1) !== '/') {
      url += '/';
    }
    return url;
  },
});