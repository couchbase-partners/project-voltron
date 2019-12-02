import {
    IonButtons,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardSubtitle,
    IonCardTitle,
    IonContent,
    IonHeader,
    IonIcon,
    IonItem,
    IonLabel,
    IonList,
    IonListHeader,
    IonMenuButton,
    IonPage,
    IonTitle,
    IonToolbar
    } from '@ionic/react';
  import { book, build, colorFill, grid } from 'ionicons/icons';
  import React, { useEffect } from 'react';
  import {TitleDetails} from '../components/TitleDetails'
  import './Home.css';
  import { async } from 'q';
  
  //const TitlePage: React.FC = () => {
  class TitlePage extends React.Component<any, any>  {

    constructor(props: any) {
        super(props)
        this.state = {
            titleInfo: null,
            notFound: '',
        }
    }
  
    getPage = async (id : string) => {
        try {
            await fetch('http://127.0.0.1:5000/api/v1/title?id=title::' + id).then(resp => resp.json()).then(data => {
                this.setState({titleInfo: data})
            })
        } catch(error) {
            this.setState({notFound: 'Title not found.'})
            console.log(error)
        }
    }
  
    componentDidMount() {
        if (this.props.match.params.id) {
            this.getPage(this.props.match.params.id)
        }        
    }

    render() {

        console.log(this.state.titleDetails)

        return (
            <IonPage>
            <IonHeader>
                <IonToolbar>
                <IonButtons slot="start">
                    <IonMenuButton />
                </IonButtons>
                <IonTitle>Title</IonTitle>
                </IonToolbar>
            </IonHeader>
            <IonContent>
                {this.state.notFound &&
                    <h1>{this.state.notFound}</h1>
                }
             <TitleDetails titleDetails={this.state.titleInfo}></TitleDetails>
            </IonContent>
            </IonPage>
        );
    }
}
  
  export default TitlePage;
  