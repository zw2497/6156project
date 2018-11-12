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
    $scope.logo = null;
    localserver = "http://localhost:5000";
    localstatic = "http://localhost:3000"
    eb = "http://6156.us-east-2.elasticbeanstalk.com";
    lambdaprofile = "https://kp1extjemk.execute-api.us-east-2.amazonaws.com/v1/6156task2";
    s3 = "http://6156static.s3-website.us-east-2.amazonaws.com"

    eb = localserver;
    s3 = localstatic;
    var init = function () {
        let claim = $window.sessionStorage.getItem("credentials");
        if (claim){
            $scope.login = 0;
            $scope.profile = 1;
            $scope.profiledetail = 0;
            $scope.res = "token :" + claim;
        }
    }
    init();
    //
    // var getUrlParam =function (parameter, defaultvalue){
    //     var urlparameter = defaultvalue;
    //     if($window.location.href.indexOf(parameter) > -1){
    //         urlparameter = getUrlVars()[parameter];
    //     }
    //     return urlparameter;
    // }
    //
    // function getUrlVars() {
    //     var vars = {};
    //     var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
    //         vars[key] = value;
    //     });
    //     return vars;
    // }
    //
    //
    // let token = getUrlParam('', null)

    console.log("Controller loaded!");


    $scope.driveLogin = function() {
        console.log("In login.");
        console.log("Email = " + $scope.email);
        console.log("Password = " + $scope.password);
        req = {
            email: $scope.email,
            pw: $scope.password
        };

        parameter = JSON.stringify(req);

        console.log("parameter = " + parameter);
        op = "login";
        url = eb + "/auth/login";


        $http.post(url, parameter, {
            headers : {
                'Content-Type': 'application/json'
            }
        }).then(
            function(result) {
                $scope.res = "Token:" + result.data.authorization + "confirm:" + result.data.confirm;
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
        url = eb + "/auth/register";


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
        let claim = $window.sessionStorage.getItem("credentials");
        let config = {}
        config.headers = { "credentials": claim, 'Content-Type': 'application/json'}
        $http.get(lambdaprofile, config).then(
            function(result) {
                console.log("Result = " + JSON.stringify(result));
                $scope.login = null;
                $scope.profile = null;
                $scope.profiledetail = 1;
                $scope.customerInfo = result.data.body;
                $scope.res = result.data.body;
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

        let claim = $window.sessionStorage.getItem("credentials");
        let config = {};
        config.headers = { "credentials": claim, 'Content-Type': 'application/json'};

        $http.post(lambdaprofile, req, config).then(
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


    $scope.googlelogin=function() {
        gapi.load('auth2', function() {
            auth2 = gapi.auth2.init({
                client_id: "1076764154881-jq0lgjdbeje9b5tsucimo3l8p48uen0v.apps.googleusercontent.com",
                scope: "email",
                ux_mode: "popup",
                redirect_uri: s3
            });

            // Sign the user in, and then retrieve their ID.
            auth2.signIn().then(function() {
                console.log("success");
                var profile = auth2.currentUser.get().getBasicProfile();
                $scope.profile = 1;
                $scope.login = 0;
                $scope.res = 'ID: ' + profile.getId() + 'Name: ' + profile.getName() + 'Email: ' + profile.getEmail()
                let token = auth2.currentUser.Ab.Zi.id_token
                $scope.googleloginhulper(token);
            }, function() {
                    console.log("failed");
                });


        });
    };

    $scope.googleloginhulper = function(id_token) {
        var xhr = new XMLHttpRequest();
        url = eb + '/auth/google';
        xhr.open('POST', url);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
            let result = xhr.responseText;
            console.log(result);
            console.log(typeof result)
            result = JSON.parse(result)
            if (result.code == 1) {
                $scope.login = 0;
                $scope.profile = 1;
                $scope.profiledetail = 0;
                $scope.$digest();
                let authorization = result.authorization;
                console.log(typeof authorization);
                console.log(authorization);
                $window.sessionStorage.setItem("credentials", authorization);
            }
        };
        xhr.send('idtoken=' + id_token);

    }

    $scope.reloadRoute = function() {
        $window.location.reload();
    }

    $scope.logout = function() {
        $window.sessionStorage.removeItem('credentials');
        $window.location.reload();
    }



});