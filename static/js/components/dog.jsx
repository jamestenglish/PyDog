var DogDesc = React.createClass({
    getInitialState: function() {
        return {overflowed: false,
                expanded: false}
    },
    componentDidMount: function() {
        var node = React.findDOMNode(this.refs.desc);
        if(parseInt(window.getComputedStyle(node).height, 10) > 120) {
            this.setState({overflowed: true});
        }
    },
    handleExpand: function() {
        this.setState({expanded: !this.state.expanded});
    },
    render: function () {

        var descClasses = classNames('desc', {'desc-overflow': this.state.overflowed && !this.state.expanded});

        var expandButton = (<span />);

        if(this.state.overflowed) {
            if(this.state.expanded) {
                expandButton = (<p><button onClick={this.handleExpand} className="btn btn-small">Collapse</button></p>)
            } else {
                expandButton = (<p><button onClick={this.handleExpand} className="btn btn-small">Expand</button></p>)
            }
        }

        return (
            <div>
                <p className={descClasses} ref="desc">{this.props.data.desc}</p>
                {expandButton}

            </div>

        );
    }
});


var DogLinks = React.createClass({
    render: function () {
        var links = this.props.data['url'].map(function(url) {
            return (<li key={url} className="link-overflow"><a href={url}>{url}</a></li>);
        });
        return (
            <p>
                <ul >
                    {links}
                </ul>
            </p>
            );
    }
});

var Dog = React.createClass({
    render: function () {
        return (
            <div className="dog col-md-4">
                <div className="thumbnail">
                    <img className="img-thumbnail" src={this.props.data.img} />
                    <div className="caption">
                        <h3 className="dogName">
                            {this.props.data.name}
                        </h3>
                        <p>{this.props.data.breed} | {this.props.data.age}</p>
                        <p>{this.props.data.size}</p>
                        <DogDesc data={this.props.data} />
                        <DogLinks data={this.props.data} />
                        <p>{this.props.data.agency}</p>

                    </div>
                </div>
            </div>
            );
    }
});