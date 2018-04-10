export default function() {

  // These comments are here to help you get started. Feel free to delete them.

  /*
    Config (with defaults).

    Note: these only affect routes defined *after* them!
  */

  // this.urlPrefix = '';    // make this `http://localhost:8080`, for example, if your API is on a different server
  this.namespace = '/api'; // make this `/api`, for example, if your API is namespaced
  // this.timing = 400;      // delay for each request, automatically set to 0 during testing

  /*
    Shorthand cheatsheet:

    this.get('/posts');
    this.post('/posts');
    this.get('/posts/:id');
    this.put('/posts/:id'); // or this.patch
    this.del('/posts/:id');

    http://www.ember-cli-mirage.com/docs/v0.3.x/shorthands/
  */
  this.get('/sitters', () => {
    return {
      count: 3,
      page_count: 18,
      next: null,
      previous: null,
      results: [{
        id: 1,
        name: 'Zelda',
        image: "http://placekitten.com/g/500/500?user=92",
        ratings_score: 3.25,
      }, {
        id: 2,
        name: 'Link',
        image: "http://placekitten.com/g/500/500?user=306",
        ratings_score: 3.333333333333,
      }, {
        id: 3,
        name: 'Epona',
        image: "http://placekitten.com/g/500/500?user=313",
        ratings_score: 4.736525,
      }]
    };
  });

}