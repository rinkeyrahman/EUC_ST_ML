from firebase import firebase


class FireBase:
    """
    Firebase is a cloud services provider and backend as a service company.
    Read more in the :ref:https://en.wikipedia.org/wiki/Firebase.
    This class is used for triggering the services from Firebase application.
    Sends the generated insights to Firebase according to service domain.

    Parameters
    ----------
    domain : list
             List of domains. [domain, subdomain1, subdomain2, ...]

    insight : string.
              Generated insight from machine learning algorithm.
    """

    def __init__(self, domain, insight):
        self.domain = domain
        self.insight = insight

    def export_insights(self):
        """
        Export the insight generated from ML algorithm to Firebase application.
        Application url : https://user-notifier.firebaseio.com

        :return:
        result : string
                 Exported insight.
        """
        # Connect to Firebase application.
        connect = firebase.FirebaseApplication('https://user-notifier.firebaseio.com', None)
        print "Send data to fire base for service calling...."
        # Put the insight value in service domain.
        result = connect.put('/user/user2', self.domain[1] + "_status", self.insight[0])
        print "Firebase result: ", result
        return result
