CustomerApp = angular.module('CustomerApp', [
    'ngRoute'
]);

CustomerApp.controller("myCtrl", function($scope, $http, $location, $window) {

    $scope.email = null;
    $scope.password = null;
    $scope.res = null;
    $scope.login = 1;
    $scope.profile = null;
    $scope.profiledetail = null;
    local1 = "http://6156.us-east-2.elasticbeanstalk.com"

    console.log("Controller loaded!")
    $scope.driveLogin = function() {
        console.log("In login.")
        console.log("Email = " + $scope.email)
        console.log("Password = " + $scope.password)
        req = {
            email: $scope.email,
            pw: $scope.password
        };

        parameter = JSON.stringify(req);

        console.log("parameter = " + parameter)
        op = "login";
        url = local1 + "/auth/login";


        $http.post(url, parameter, {
            headers : {
                'Content-Type': 'application/json'
            }
        }).then(
            function(result) {
                $scope.res = "Token:" + result.data.authorization;
                if (result.data.code == 1) {
                    $scope.login = 0;
                    $scope.profile = 1;
                    $scope.profiledetail = 0;
                    let authorization = result.data.authorization;
                    console.log(typeof authorization)
                    console.log(authorization)
                    $window.sessionStorage.setItem("credentials", authorization);
                }
            },
            function(error) {
                console.log("Result = " + JSON.stringify(error));
            }

        );
    };
    $scope.driveRegister = function() {
        console.log("I am Register.");
        req = {
            email: $scope.email,
            pw: $scope.password
        };

        parameter = JSON.stringify(req);

        console.log("parameter = " + parameter)
        op = "register";
        url = local1 + "/auth/register";


        $http.post(url, parameter, {
            headers : {
                'Content-Type': 'application/json'
            }
        }).then(
            function(result) {
                console.log("Result = " + JSON.stringify(result));
                $scope.res = result.data.body;
                if (result.data.code == 1) {
                    $scope.login = 1;
                    $scope.profile = 0;
                    $scope.profiledetail = 0;
                }
            },
            function(error) {
                console.log("Result = " + JSON.stringify(error));
            }

        );

    }
    $scope.getprofile = function() {
        console.log("help")
        url = "https://kp1extjemk.execute-api.us-east-2.amazonaws.com/v1/6156task2"
        let claim = $window.sessionStorage.getItem("credentials");
        let config = {}
        config.headers = { "credentials": claim, 'Content-Type': 'application/json'}
        $http.get(url, config).then(
            function(result) {
                console.log("Result = " + JSON.stringify(result));
                $scope.login = null;
                $scope.profile = null;
                $scope.profiledetail = 1;
                $scope.customerInfo = result.data.body;
                console.log("success")
            }, function(result) {
                console.log("fail")
            }, function (response) {
                console.log("what?")
            }
            );
    }

    $scope.toupdateprofile = function() {
        console.log("update")
        $scope.profiledetail = 0;
        $scope.update = 1;

    }

    $scope.updateprofile = function() {
        req = {
            phone: $scope.phone,
            address: $scope.address
        };

        url = "https://kp1extjemk.execute-api.us-east-2.amazonaws.com/v1/6156task2";

        let claim = $window.sessionStorage.getItem("credentials");
        let config = {};
        config.headers = { "credentials": claim, 'Content-Type': 'application/json'};

        $http.post(url, req, config).then(
            function(result) {
                console.log("Result = " + JSON.stringify(result));
                $scope.res = result.data.body;
                if (result.data.code == 1) {
                    $scope.profile = 1;
                    $scope.update = 0;
                }
            },
            function(error) {
                console.log("Result = " + JSON.stringify(error));
            }

        );

    }

});