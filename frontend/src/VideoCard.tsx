import React, { Component } from 'react'

interface IProps {
    title: string,
    description: string,
    thumbnail: string,
    publishedAt: string,
    channel: string,
    videoId: string
}

export default class VideoCard extends Component<IProps, {}> {
    constructor(props: IProps) {
        super(props)

        this.state = {

        }
    }

    render() {
        const { thumbnail, title, description, publishedAt, channel, videoId } = this.props;
        return (
            <a href={`https://www.youtube.com/watch?v=${videoId}`} className="list-group-item list-group-item-action" target="_blank">
                <div className="card bg-light mb-3">
                    <div className="row no-gutters">
                        <div className="col-md-4">
                            <img src={thumbnail} className="card-img" alt="..." />
                        </div>
                        <div className="col-md-8">
                            <div className="card-body text-left">
                                <h5 className="card-title">{title}</h5>
                                <p className="card-text"><span className="h5">Description: </span> {description}</p>
                                <div className="row">
                                    <div className="col">
                                        <h5 className="card-text">{channel}</h5>
                                    </div>
                                    <div className="col">
                                        <p className="card-text">{new Date(Date.parse(publishedAt)).toLocaleString()}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </a>
        )
    }
}
