var map;
var mapvm;

$(document).ready(function () {

    createMap();
    mapvm = new mapViewModel()
    ko.applyBindings(mapvm);


});

function createMap() {
    var elevator;
    var myOptions = {
        zoom: 7,
        center: new google.maps.LatLng(39.201312, -105.788901),
        mapTypeId: 'terrain'
    };
    map = new google.maps.Map($('#map')[0], myOptions);

   
 
    google.maps.event.addListener(map,'click',function(point)
    {
        document.getElementById('latlongclicked').value = point.latLng
    });

}

function Legend(data) {
    this.low_rating = ko.observable(data.low_rating);
    this.high_rating = ko.observable(data.high_rating);
    this.scenery = ko.observable(data.scenery);
    this.elevation = ko.observable(data.elevation);
    this.rock_crawling = ko.observable(data.rock_crawling);
    this.climbs_descents = ko.observable(data.climbs_descents);
    this.water_crossing = ko.observable(data.water_crossing);
    this.cliffs_ledges = ko.observable(data.cliffs_ledges);
    this.dirt_mud = ko.observable(data.dirt_mud);
    this.playgrounds = ko.observable(data.playgrounds);
}

function Trail(data) {

    this.name = ko.observable(data.name);
    this.id = ko.observable(data.id);
    this.my_last_time = ko.observable(data.my_last_time);
    this.my_note = ko.observable(data.my_note);
    this.lat = ko.observable(data.lat_lng[0]);
    this.long = ko.observable(data.lat_lng[1]);
    this.directions = ko.observable(data.directions);
    this.legend = ko.observable(new Legend(data.legend));

    this.nearby_towns = ko.observable(data.nearby_towns);
    this.nearby_trails = ko.observable(data.nearby_trails);
    this.elevation = ko.observable(data.elevation);
    this.trail_length = ko.observable(data.trail_length);
    this.trail_type = ko.observable(data.trail_type);
    this.county = ko.observable(data.county);
    this.updated = ko.observable(data.updated);

    if (data.ibeen_there == "been_there") {
        this.marker = new google.maps.Marker({
            position: new google.maps.LatLng(data.lat_lng[0], data.lat_lng[1]),
            title: data.name,
            icon: "/images/blue-dot.png",
            map: map,
        });
    }
    else if (data.ibeen_there == "never_there") {
        this.marker = new google.maps.Marker({
            position: new google.maps.LatLng(data.lat_lng[0], data.lat_lng[1]),
            title: data.name,
            icon: "/images/red-dot.png",
            map: map,
        });
    }
    else if (data.ibeen_there == "warning") {
        this.marker = new google.maps.Marker({
            position: new google.maps.LatLng(data.lat_lng[0], data.lat_lng[1]),
            title: data.name,
            icon: "/images/marker_yellow.png",
            map: map,
        });
    }
    else if (data.ibeen_there == "i_added") {
        this.marker = new google.maps.Marker({
            position: new google.maps.LatLng(data.lat_lng[0], data.lat_lng[1]),
            title: data.name,
            icon: "/images/marker_green.png",
            map: map,
        });
    }

    google.maps.event.addListener(this.marker, 'click', function () {
        //map.setZoom(8);
        //map.setCenter(marker.getPosition());
        //mapvm.ShowTrail(this.marker.getTitle());
        var newObject = $.extend(true, {}, this);
        mapvm.ShowTrail(newObject);
    }.bind(this));
}

ko.bindingHandlers.starRating = {
    init: function (element, valueAccessor) {
        $(element).addClass("starRating");
        for (var i = 0; i < 10; i++)
            $("<span>").appendTo(element);
    },
    update: function (element, valueAccessor) {
        // Give the first x stars the "chosen" class, where x <= rating
        var observable = valueAccessor();
        $("span", element).each(function (index) {
            $(this).toggleClass("chosen", index < observable());
        });
    }
};

function mapViewModel() {
    var self = this

    self.filt_low_end = ko.observable(0);
    self.filt_length = ko.observable(0);
    self.filt_type = ko.observable("None");
    self.filt_rock = ko.observable(0);
    self.filt_climbs = ko.observable(0);
    self.filt_water = ko.observable(0);
    self.filt_cliffs = ko.observable(0);
    self.filt_dirt = ko.observable(0);
    self.filt_play = ko.observable(0);
    self.filt_scene = ko.observable(0);
    self.filt_elevation = ko.observable(0);

    self.trails = ko.observableArray([]);
    self.selected_trail = ko.observable();

    $.getJSON("/markers", function (allData) {
        var mappedTasks = $.map(allData, function (item) { return new Trail(item) });
        self.trails(mappedTasks);
    });

   
    self.ShowTrail = function (t) {       
        var match = ko.utils.arrayFirst(self.trails(), function (item) {
            return t.name() === item.name();
        });
        self.selected_trail(t);
    };



    self.FilterStuff = function () {
        for (var i = 0; i < self.trails().length; i++) {
            self.trails()[i].marker.setMap(null);
        }
        self.trails.removeAll();
        $.getJSON("/markers", function (allData) {
            var mappedTasks = $.map(allData, function (item) {
                var le = self.filt_low_end();
                if ((item.legend.low_rating >= self.filt_low_end()) &&
                     (item.trail_length >= self.filt_length()) &&
                     (item.legend.rock_crawling >= self.filt_rock()) &&
                     (item.legend.climbs_descents >= self.filt_climbs()) &&
                     (item.legend.water_crossing >= self.filt_water()) &&
                     (item.legend.cliffs_ledges >= self.filt_cliffs()) &&
                     (item.legend.dirt_mud >= self.filt_dirt()) &&
                     (item.legend.playgrounds >= self.filt_play()) &&
                     (item.legend.scenery >= self.filt_scene()) &&
                     (item.legend.elevation >= self.filt_elevation())) {

                    if (self.filt_type() != 'None') {
                        if (self.filt_type() == item.trail_type) {
                            return new Trail(item);
                        }
                    } else {
                        return new Trail(item);
                    }
                }
                return null;
            });
            self.trails(mappedTasks);
        });
    }

};

