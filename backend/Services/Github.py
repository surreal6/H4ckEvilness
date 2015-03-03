from Services.ServiceModel import ServiceModel


class GithubModel(ServiceModel):

    def populate_candidate(self):
        super(GithubModel, self).populate_candidate()
        if self.url_profile:
            self.nick = self.url_profile[self.url_profile.rfind("/")+1:]