from locust import HttpUser, task, between

class SamTMUser(HttpUser):
    wait_time = between(0.5, 2.0)
    token = "SET_TEST_TOKEN"
    school_id = 16

    @task(5)
    def me(self):
        self.client.get(f"/auth/men?token={self.token}", name="/auth/men")

    @task(4)
    def school_dashboard(self):
        self.client.get(f"/api/maktab/dashboard?token={self.token}&maktab_id={self.school_id}", name="/api/maktab/dashboard")

    @task(2)
    def timetable_setup(self):
        self.client.get(f"/api/maktab/aqlli_jadval/v2/sozlamalar?token={self.token}&maktab_id={self.school_id}", name="/api/maktab/aqlli_jadval/v2/sozlamalar")

    @task(1)
    def live(self):
        self.client.get("/health/live")
