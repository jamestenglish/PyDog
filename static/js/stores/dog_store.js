var DogStore = Reflux.createStore({
    listenables: [DogActions, CommonActions],
    init: function () {
        this.listenTo(CommonActions.load, this.fetchData);
        this.listenTo(DogActions.load, this.fetchData);
        this.listenTo(DogActions.filter, this.filterData);
    },
    getInitialState: function () {
        this.list = [];
        this.filter = '';
        return this.list;
    },
    filterData: function(filter) {
        this.filter = filter;
        this.trigger(this._filterData(this.list));
    },
    _filterData: function(list) {
        var filter_list = this.filter.split(" ");
        return list.filter(function(item) {
            for(var i=0; i<filter_list.length; i++) {
                var filter_string = filter_list[i].trim().toLowerCase();
                if(filter_string.length == 0) {
                    return true;
                }
                if(item['breed'].toLowerCase().indexOf(filter_string) > -1) {
                    return false
                }
            }
            return true;
        });
    },
    fetchData: function () {
        $.ajax({
            url: '/dogs/',
            dataType: 'json',
            success: function (dogs) {
                this.updateList(dogs);
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(status, err.toString());
            }.bind(this)
        });
    },
    updateList: function (list) {
        this.list = list;
        this.trigger(this._filterData(list));
    }
});