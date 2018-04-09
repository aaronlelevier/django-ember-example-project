import DS from 'ember-data';

export default DS.RESTSerializer.extend({
  normalizeResponse: function(store, primaryModelClass, payload, id, requestType) {
    payload[primaryModelClass.modelName] = payload.results;
    delete payload.results;

    return this._super(store, primaryModelClass, payload, id, requestType);
  }
});