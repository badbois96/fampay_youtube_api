import React, { Component } from 'react';
import axios from 'axios';
import VideoCard from './VideoCard'

interface APIData {
    title: string,
    description: string,
    thumbnail: string,
    publishedAt: string,
    channel: string
}

interface IState {
    query: string,
    description: string,
    page: number,
    dataList: Array<any>,
    dataLoaded: boolean
}

export default class Dashboard extends Component<{}, IState> {
    constructor(props: {}) {
        super(props)

        this.state = {
            query: "",
            description: "",
            page: 1,
            dataList: [],
            dataLoaded: false
        }
    }


    fetchData = () => {

        const { query, description, page } = this.state;

        let url = `http://127.0.0.1:8000/getvideos/?q=${query}&desc=${description}&page=${page}`
        axios.get(url)
            .then(res => {
                // console.log(res.data['result']);
                this.setState({
                    dataLoaded: true,
                    dataList: res.data['result']
                });
            })
            .catch(error => {
                console.error(error);
            });
    }

    prev = () => {
        const { page } = this.state;
        this.setState({
            page: page - 1
        }, this.fetchData);
    }

    next = () => {
        const { page } = this.state;
        this.setState({
            page: page + 1
        }, this.fetchData);
    }

    componentDidMount() {
        this.fetchData();
    }

    render() {
        const { dataList, dataLoaded } = this.state;
        // console.log(typeof (dataList));
        return (
            <div className="jumbotron jumbotron-fluid bg-transparent m-0">
                <h3 className="display-4 pb-5">Youtube API</h3>
                <div className="container container-fluid p-5">
                    <div className="input-group mb-3">
                        <input type="text" className="form-control" placeholder="What do you wanna watch today?"
                            aria-label="What do you wanna watch today?" aria-describedby="button-addon2"
                            onChange={(event) => this.setState({ query: event.target.value })}
                            value={this.state.query}
                        />
                        <div className="input-group-append">
                            <button className="btn btn-outline-secondary" type="button" onClick={this.fetchData}>Search</button>
                        </div>
                    </div>
                    <div className="list-group">
                        {dataLoaded ?
                            dataList.map((item, key) => {
                                return <VideoCard key={key} title={item.title} description={item.description}
                                    publishedAt={item.published_at} thumbnail={item.thumbnail_url}
                                    videoId={item.video_id} channel={item.channel_title}
                                />
                            }) : null
                        }
                    </div>
                    <div className="input-group justify-content-center mt-3">
                        <div className="input-group-append">
                            <button className="btn btn-outline-secondary" type="button" onClick={this.prev}>Prev</button>
                        </div>
                        <div className="input-group-append">
                            <button className="btn btn-outline-secondary" type="button" onClick={this.next}>Next</button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
