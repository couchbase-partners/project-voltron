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
  IonToolbar
} from '@ionic/react';
import React from 'react';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { AppPage } from '../declarations';
import { home, list } from 'ionicons/icons';

interface MenuProps extends RouteComponentProps {
  appPages: AppPage[];
}

const Menu: React.FunctionComponent<MenuProps> = ({ appPages }) => (
  <IonMenu contentId="main" type="overlay">
    <IonHeader>
      <IonToolbar>
        <IonTitle>Menu</IonTitle>
      </IonToolbar>
    </IonHeader>
    <IonContent>
      <IonList>
        <IonMenuToggle autoHide={false}>
          <IonItem routerLink='/home' routerDirection="none">
                <IonIcon slot="start" icon={home} />
                <IonLabel>Home</IonLabel>
              </IonItem>
        </IonMenuToggle>

        <IonMenuToggle autoHide={false}>
          <IonItem routerLink='/home/list' routerDirection="none">
                <IonIcon slot="start" icon={list} />
                <IonLabel>List</IonLabel>
              </IonItem>
        </IonMenuToggle>

        {/*appPages.map((appPage, index) => {
          return (
            <IonMenuToggle key={index} autoHide={false}>
              <IonItem routerLink={appPage.url} routerDirection="none">
                <IonIcon slot="start" icon={appPage.icon} />
                <IonLabel>{appPage.title}</IonLabel>
              </IonItem>
            </IonMenuToggle>
          );
        })*/}
      </IonList>
    </IonContent>
  </IonMenu>
);

export default withRouter(Menu);
