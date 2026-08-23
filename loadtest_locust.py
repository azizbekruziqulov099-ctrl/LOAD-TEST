"""SamTM V19.2 read/load smoke test, including teacher-first endpoints."""

import os

from locust import HttpUser, task, between

class SamTMUser(HttpUser):
    wait_time = between(0.5, 2.0)
    token = os.getenv("SAMTM_TEST_TOKEN", "SET_TEST_TOKEN")
    school_id = int(os.getenv("SAMTM_TEST_SCHOOL_ID", "16"))
    timetable_run_id = int(os.getenv("SAMTM_TEST_TIMETABLE_RUN_ID", "0"))
    timetable_slot_id = int(os.getenv("SAMTM_TEST_TIMETABLE_SLOT_ID", "0"))

    @task(1)
    def version(self):
        self.client.get("/api/versiya", name="/api/versiya")

    @task(5)
    def me(self):
        self.client.get(f"/auth/men?token={self.token}", name="/auth/men")

    @task(4)
    def school_dashboard(self):
        self.client.get(f"/api/maktab/dashboard?token={self.token}&maktab_id={self.school_id}", name="/api/maktab/dashboard")

    @task(2)
    def timetable_setup(self):
        self.client.get(f"/api/maktab/aqlli_jadval/v2/sozlamalar?token={self.token}&maktab_id={self.school_id}", name="/api/maktab/aqlli_jadval/v2/sozlamalar")

    @task(3)
    def teacher_load_matrix(self):
        self.client.get(
            f"/api/maktab/aqlli_jadval/v3/yuklama_matritsasi?token={self.token}&maktab_id={self.school_id}",
            name="/api/maktab/aqlli_jadval/v3/yuklama_matritsasi",
        )

    @task(1)
    def smart_swap_suggestions(self):
        if not self.timetable_run_id or not self.timetable_slot_id:
            return
        self.client.get(
            "/api/maktab/aqlli_jadval/v3/almashtirish_tavsiyalari",
            params={
                "token": self.token,
                "urinish_id": self.timetable_run_id,
                "slot_id": self.timetable_slot_id,
            },
            name="/api/maktab/aqlli_jadval/v3/almashtirish_tavsiyalari",
        )

    @task(1)
    def live(self):
        self.client.get("/health/live")
