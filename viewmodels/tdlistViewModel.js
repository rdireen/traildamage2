function tdlistViewModel() {
    var self = this

    self.trails = ko.observable([]);

    $.getJSON("/markers", function (allData) {
        var mappedTasks = $.map(allData, function (item) { return new Trail(item) });
        self.trails(mappedTasks);
    });

};