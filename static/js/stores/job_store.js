var JobStore = Reflux.createStore({
    listenables: [JobActions],
    init: function () {
        this.listenTo(JobActions.load, this.fetchData);
        this.listenTo(JobActions.post, this.postData);
    },
    getInitialState: function () {
        this.data = {};
        return this.data;
    },
    fetchData: function (id) {
        $.ajax({
            url: '/jobs/dog_scrape/' + id + '/',
            dataType: 'json',
            success: function (result) {
                this.updateData(result);
                if(!result['done']) {
                    setTimeout(function() {
                        JobActions.load(id);
                    }, 1000)
                } else {
                    DogActions.load();
                }
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(status, err.toString());
            }.bind(this)
        });


    },
    postData: function () {
        $.ajax({
            url: '/jobs/dog_scrape/',
            method: 'POST',
            dataType: 'json',
            success: function (result) {
                if(result.hasOwnProperty('job_id')) {
                    setTimeout(function() {
                        JobActions.load(result['job_id']);
                    }, 500);
                }
                this.updateData(result);
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(status, err.toString());
            }.bind(this)
        });
    },
    updateData: function (data) {
        this.data = data;
        this.trigger(data);
    }
});