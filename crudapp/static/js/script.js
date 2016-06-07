$(document).ready(function() {
  $('.report').one('click', function() {
    // var message = prompt("Let us know why you are reporting this post.")
    var id = this.id;
    $.get("/report/" + id + "/", function(data) {
      $('#reported' + id).html('post has been reported');
    });
  });
      $('.vote_up').one('click', function() {
        var id = this.id;
        $.get("/vote_up/" + id + "/", function(data) {
          $('#voted' + id).html(data);
        });
      });
      $('.vote_down').one('click', function() {
        var id = this.id;
        $.get("/vote_down/" + id + "/", function(data) {
          $('#voted' + id).html(data);
        });
      });
      $('.vote_up_article').one('click', function() {
        var id = this.id;
        $.get("/vote_up_article/" + id + "/", function(data) {
          $('#voted' + id).html('Votes ' + data);
        });
      });
      $('.vote_down_article').one('click', function() {
        var id = this.id;
        $.get("/vote_down_article/" + id + "/", function(data) {
          $('#voted' + id).html('Votes ' + data);
        });
      });
      $('.vote_up_file').one('click', function() {
        var id = this.id;
        $.get("/vote_up_file/" + id + "/", function(data) {
          $('#voted' + id).html('Votes ' + data);
        });
      });
      $('.vote_down_file').one('click', function() {
        var id = this.id;
        $.get("/vote_down_file/" + id + "/", function(data) {
          $('#voted' + id).html('Votes ' + data);
        });
      });
    });
