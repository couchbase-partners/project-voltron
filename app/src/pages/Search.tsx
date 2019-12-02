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
  import React, { useEffect, useState } from 'react';
  import {TitleDetails} from '../components/TitleDetails'
  import './Home.css';
  import { async } from 'q';
  import queryString from 'querystring'

  const Search: React.FC = (props : any) => {

    const [query, setQuery] = useState('')
    const [results, setResults] = useState({})

    useEffect(() => {
        const values = queryString.parse(props.location.search)
        setQuery(values['?q'].toString())
    }, [props.location.search])

    useEffect(() => {
        async function fetchResults() {
            fetch('http://127.0.0.1:5000/api/v1/search?q=' + query).then(resp => resp.json()).then(data => {
                console.log(data)
                setResults(data)                    
            })
        }
        if (query.length > 0) {
            fetchResults()
        }
    }, [query])

    return (
        <div>Search page: {query}            
        </div>
    )
  }

  export default Search