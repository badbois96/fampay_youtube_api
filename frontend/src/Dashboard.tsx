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
    maxPage: number,
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
            dataLoaded: false,
            maxPage: Infinity
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
                    dataList: res.data['result'],
                    maxPage: res.data['total_page']
                });
            })
            .catch(error => {
                console.error(error);
            });
    }

    newSearch = () => {
        this.setState({
            page: 1
        }, this.fetchData);
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
        const { dataList, dataLoaded, page, maxPage } = this.state;

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
                            <button className="btn btn-outline-secondary" type="button" onClick={this.newSearch}>Search</button>
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
                            <button className="btn btn-outline-secondary" type="button" disabled={page < 2} onClick={this.prev}>Prev</button>
                        </div>
                        <div className="input-group-append">
                            <button className="btn btn-outline-secondary" type="button" disabled={page >= maxPage} onClick={this.next}>Next</button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
