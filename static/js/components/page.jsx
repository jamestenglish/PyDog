var Page = React.createClass({
    mixins: [Reflux.connect(DogStore, "dogs"),
        Reflux.connect(JobStore, "job")/*,
         Reflux.connect(ZipStore, "zip"),
         Reflux.connect(FilterStore, "filter"),
         */],


    componentDidMount: function () {
        CommonActions.load();
    },

    render: function () {
        return (
            <div>
                <nav className="navbar navbar-default navbar-static-top">
                    <div className="container">
                        <div className="navbar-header">
                            <a className="navbar-brand" href="#">PyDog</a>
                        </div>
                        <div id="navbar">
                            <Filter />
                            <ul className="nav navbar-nav navbar-right">
                                <li><Job data={this.state.job} /></li>
                            </ul>
                        </div>
                    </div>
                </nav>

                <div className="container">

                    <DogList data={this.state.dogs} />
                </div>
            </div>
            );
    }
});


React.render(
    <Page />,
    document.getElementById('Main')
);

//  getInitialState: function() {
//    return {dogs: [],
//            zip: '',
//            filter: '',
//            job: {}};
//  },