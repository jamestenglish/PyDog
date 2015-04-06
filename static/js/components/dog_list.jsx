var DogList = React.createClass({
    render: function () {

        var dogNodes = this.props.data.map(function (dog) {
            return (
                <Dog data={dog} key={dog['_id']} />
            );
        });

        var dogGroups = [];
        var size = 3;

        while (dogNodes.length > 0) {
            dogGroups.push(dogNodes.splice(0, size));
        }

        var dogRows = dogGroups.map(function(group) {
            var key = "";
            for(var i=0;i<group.length;i++) {
                key += group[i].key;
            }
            return (
                <div className="row" key={key}>{group}</div>
            );
        });



        return (
            <div className="dogList row">
                {dogRows}
            </div>
            );
    }
});