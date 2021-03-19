// CRUD service for Notes model note
app.service('$cars', function($http) {
    this.cars_api_uri = '/api/car/';
    this.default_options = function(url_ending, data) {
        return {
            url: [this.cars_api_uri, url_ending].join(""),
            method: 'POST',
            data: data
        };
    }

    this.get = function(titleFilter) {
        return $http(this.default_options('get', {titleFilter: titleFilter})).then(function(response) {
            return response.data;
        });
    };
	
	this.get = function(brandFilter) {
        return $http(this.default_options('get', {brandFilter: brandFilter})).then(function(response) {
            return response.data;
        });
    };

    this.create = function(data) {
        return $http(this.default_options('create', data)).then(function(response) {
            return response.data;
        });
    };

    this.modify = function(id, data) {
        return $http(this.default_options('modify/'+id, data)).then(function(response) {
            return response.data;
        });
    };

    this.delete = function(id) {
        return $http(this.default_options('delete/'+id, {})).then(function(response) {
            return response.data;
        });
    };

    this.getById = function(id) {
        return $http(this.default_options('get', {id: id})).then(function(response) {
            return response.data;
        });
    }
});

// Custom navigation service
app.service('$navigate', function() {
    this.goBack = function() {
        history.go(-1);
    }
    
    this.goTo = function(url) {
        window.location.href = url;
    }
})