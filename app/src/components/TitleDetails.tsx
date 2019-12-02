import {
    IonContent,
    IonHeader,
    IonIcon,
    IonItem,
    IonLabel,
    IonList,
    IonMenu,
    IonMenuToggle,
    IonTitle,
    IonToolbar,
    IonGrid,
    IonRow,
    IonCol
  } from '@ionic/react';
  import { home, list, star, starHalf } from 'ionicons/icons';
  import React, { useState, useEffect } from 'react';
  import { RouteComponentProps, withRouter } from 'react-router-dom';
  import { AppPage, omdbAPIKey } from '../declarations';

type Props = {
    titleDetails?: any
  }



export const TitleDetails: React.FC<Props> = (props) => {

    const [omdbResponse, setOmdbResponse] = useState(Object)
    useEffect(() => {
        async function fetchDetails() {
            if (props.titleDetails) {
            var id = props.titleDetails.id.replace('title::','')
                fetch('http://www.omdbapi.com/?i=' + id + '&apikey=' + omdbAPIKey).then(resp => resp.json()).then(data => {
                    setOmdbResponse(data)
                })
            }
        }
        fetchDetails()
    }, [props.titleDetails])

    if (omdbResponse && omdbResponse!.Actors) {
        return (
                <IonGrid>
                <IonRow>
                    <IonCol size="2">
                        <img src={omdbResponse.Poster} alt={props.titleDetails.originalTitle} height={250}/>
                    </IonCol>
                    <IonCol>
                        <h1>{props.titleDetails.originalTitle}</h1>
                        <p><i>Starring </i> {omdbResponse.Actors}<br/>
                        <i>Directed by </i> {omdbResponse.Director}</p>
                        <p>
                            {omdbResponse.Plot}                    
                        </p>   
                    </IonCol>
                </IonRow>                    
                </IonGrid>
        )
    } else {
        return (<div></div>)
    }

}

/*class TitleDetails extends React.Component<Props, State> {

    constructor(props: Props) {
        super(props)
        this.state = {
            omdbResponse: null
        }
    }

    componentDidMount() {        
    }

    componentDidUpdate(prevProps : Props) {
        if (prevProps.titleDetails != this.props.titleDetails) {
            if (this.props.titleDetails) {
                var id = this.props.titleDetails.id.replace('title::','')
                fetch('http://www.omdbapi.com/?i=' + id + '&apikey=' + omdbAPIKey).then(resp => resp.json()).then(data => {
                    this.setState({omdbResponse: data})
                })
            }
        }
    }

    render() {

        console.log(this.state.omdbResponse)

        let stars

        if (this.props.titleDetails && this.state.omdbResponse) {

            let stars
            if (this.state.omdbResponse.imdbRating) {
                stars = <div> <b>Rating</b>: {this.state.omdbResponse.imdbRating} out of 10 ({this.state.omdbResponse.imdbVotes} votes)</div>
            }

            return (     
                <IonGrid>
                    <IonRow>
                        <IonCol size="2">
                               <img src={this.state.omdbResponse.Poster} alt={this.props.titleDetails.originalTitle} height={250}/>
                          </IonCol>
                          <IonCol>
                            <h1>{this.props.titleDetails.originalTitle}</h1>
                            <p><i>Starring </i> {this.state.omdbResponse.Actors}<br/>
                            <i>Directed by </i> {this.state.omdbResponse.Director}</p>
                            <p>
                                {this.state.omdbResponse.Plot}                    
                            </p>   
                            {stars}
                        </IonCol>
                    </IonRow>                    
                </IonGrid>       
            )
        }

        return <div></div>
    }

}

  export default TitleDetails*/