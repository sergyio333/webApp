// routing system for the application
// angularJS routing system works with views and controllers each seperate route can have a diff HTML tempalte (views directory) 
// and a diff Controller (app.controller) note
var app = angular.module('appTitleGoesHere', [], function ($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', { templateUrl: "./views/default.html", controller: "DefController" })
        .when('/table', { templateUrl: "./views/empty.html", controller: "EmptyController" })
        .when('/preview/:id', { templateUrl: "./views/car_preview.html", controller: "PreviewController" })
        .when('/edit/:id', { templateUrl: "./views/car_form.html", controller: "carModifyController" })
        .when('/create', { templateUrl: "./views/car_form.html", controller: "carCreateController" })
        .otherwise({ redirectTo: "/" });

    $locationProvider.html5Mode(false);

});

// global controller object
function MainCtrl($scope, $route, $routeParams, $navigate, $location) {
    $scope.$route = $route;
    $scope.$location = $location;
    $scope.$routeParams = $routeParams;
    $scope.home = function() {
        $navigate.goTO("/#/")
    }
    $scope.table = function(){
        $navigate.goTo("/#/table");
    }
}


// home page controller (shows all the cars in the database)
app.controller('DefController', function ($scope, $navigate, $cars, $timeout) {
    $scope.cars = [];
    $scope.filterText = "";
    $scope.fuelFilter = "";
    $scope.init = function() {
        $cars.get($scope.filterText ).then(function(result) {
            $scope.cars = result;
        });
    }
    $scope.sort = function() {
        $cars.get($scope.fuelFilter ).then(function(result) {
            $scope.cars = result;
        });
    }

    // timeout is used to avoid consant server calls (instead we use the debounce method)
    var _timeout = null;
    $scope.filter = function() {
        if(_timeout) { // if there is already a timeout in process cancel it
            $timeout.cancel(_timeout);
        }
        _timeout = $timeout(function() {
            $scope.init();
            _timeout = null;
        }, 800);
    }

    $scope.createcar = function() {
        $navigate.goTo("/#/create");
    }

    $scope.looktable = function() {
        $navigate.goTo("/#/table");
    }

    $scope.modifycar = function(id) {
        $navigate.goTo(["/#/edit/", id].join(""));
    }

    $scope.previewcar = function(id) {
        $navigate.goTo(["/#/preview/", id].join(""));
    }

    $scope.deletecar = function(id) {
        if (confirm("Are you sure you want to delete this car?")) {
            $cars.delete(id).then(function(result) {
                alert("car was deleted")
                $navigate.goTo("/#/"); // go to home page after delete
            });
        }
    }
});

//


// preview for a single car
app.controller('PreviewController', function ($scope, $navigate, $cars, $routeParams) {
    $scope.car = {};
    $scope.init = function() {
        $cars.getById($routeParams.id).then(function(result) {
            $scope.car = result;
        });
    }

    $scope.goBack = function() {
        $navigate.goBack();
    }

    $scope.modifycar = function(id) {
        $navigate.goTo(["/#/edit/", id].join(""));
    }

    $scope.deletecar = function(id) {
        if (confirm("Are you sure you want to delete this car?")) {
            $cars.delete(id).then(function(result) {
                alert("car was deleted");
                $navigate.goTo("/#/"); // go to home page after delete
            });
        }
    }
});

// form for creating cars
app.controller('carCreateController', function ($scope, $navigate, $cars) {
    $scope.init = function() {};
    $scope.car = {
        "Title": "",
        "Brand": "",
		"Model": "",
		"DrivedDistance": "",
		"Price": "",
    };

    $scope.submit = function() {
        $cars.create($scope.car).then(function(result) {
            alert("car was created!");
            $navigate.goTo("/#/");
        })
    }

    $scope.goBack = function() {
        $navigate.goBack();
    }
});

// form for modifying cars
app.controller('carModifyController', function ($scope, $navigate, $cars, $routeParams) {
    $scope.car = {};
    $scope.isEdit = true;

    $scope.init = function() {
        $cars.getById($routeParams.id).then(function(result) {
            $scope.car = result;
        });
    }

    $scope.deletecar = function(id) {
        if (confirm("Are you sure you want to delete this car?")) {
            $cars.delete(id).then(function(result) {
                alert("car was deleted");
                $navigate.goTo("/#/"); // go to home page after delete
            });
        }
    }

    $scope.submit = function() {
        $cars.modify($routeParams.id, $scope.car).then(function(result) {
            alert("car was updated!");
            $navigate.goTo(["/#/preview/", $routeParams.id].join(""));
        })
    }

    $scope.goBack = function() {
        $navigate.goBack();
    }
});
