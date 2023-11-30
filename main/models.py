from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField 
from autoslug import AutoSlugField
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    is_hr = models.BooleanField(default=False)
    is_teamlead = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_mainHr = models.BooleanField(default=False)
    is_teamMember = models.BooleanField(default=False)
    is_onboardingHr = models.BooleanField(default=False)
    released_jobs = models.ForeignKey('Job', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Job(models.Model):
    job_name = models.CharField(max_length=255)
    job_release_date = models.DateField()
    job_closing_date = models.DateField()
    job_location = models.CharField(max_length=255)
    about_company = models.TextField()
    project_role = models.CharField(max_length=255)
    project_role_desc = models.TextField()
    work_experience = models.PositiveIntegerField()
    must_have_skills = models.TextField()
    good_to_have_skills = models.TextField()
    job_requirements = models.TextField()
    qualifications = models.TextField()
    types = [
        ('FullTime', 'FullTime'),
        ('PartTime', 'PartTime'),
        ('Internship', 'Internship')
    ]
    job_type = models.CharField(max_length=100, choices=types)
    released_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    slug = AutoSlugField(populate_from='job_name', unique=True, null=True, blank=True)

    def __str__(self):
        return self.job_name
    


class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    ph_num = PhoneNumberField()
    linkedin = models.URLField(max_length=200)
    github = models.URLField(max_length=200)
    resume = models.FileField(upload_to='resumes')
    hear = models.CharField(max_length=100)
    current_city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    available_date = models.DateField()
    logs = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Create a unique and strong slug using the applicant's name and a timestamp
        timestamp_str = str(int(self.logs.timestamp()))  # Use logs or another timestamp field
        self.slug = slugify(f"{self.f_name}-{self.l_name}-{timestamp_str}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('applicant_detail', kwargs={'slug': self.slug})
    def __str__(self):
        return f"{self.f_name} {self.l_name} - {self.job.job_name}"


class MeetingSchedule(models.Model):
    job_application = models.ForeignKey('JobApplication', on_delete=models.CASCADE)
    scheduled_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    scheduled_meet_date = models.DateTimeField(null=True, blank=True)
    scheduled_meet_time = models.TimeField(null=True, blank=True)
    scheduled_meet_link = models.URLField(max_length=200, null=True, blank=True)
    scheduled_meet_attendees = models.ManyToManyField(User, related_name='meeting_attendees', blank=True)
    logs = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f"Meeting for {self.job_application.user.username}"
    
    
class MeetingReview(models.Model):
    meeting_schedule = models.ForeignKey('MeetingSchedule', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    decision = models.CharField(max_length=600)  # 'accept' or 'reject'
    reason = models.TextField()

    def __str__(self):
        applicant_name = f"{self.meeting_schedule.job_application.f_name} {self.meeting_schedule.job_application.l_name}"
        return f"Review for {applicant_name}"
    
class TeamLeadDecision(models.Model):
    ACCEPT = 'accept'
    REJECT = 'reject'
    DECISION_CHOICES = [
        (ACCEPT, 'Accept'),
        (REJECT, 'Reject'),
    ]

    applicant = models.OneToOneField(User, on_delete=models.CASCADE, related_name='decision_review', null=True, blank=True)
    decision = models.CharField(max_length=10, choices=DECISION_CHOICES)
    reason = models.TextField()
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    logs = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        if self.applicant:          
            return f"{self.applicant} - Decision: {self.decision}"
        else:
            return f"Decision: {self.decision} (No MeetingReview)"


class ManagerDecision(models.Model):
    applicant = models.CharField(max_length=255)
    decision = models.CharField(max_length=50, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    approved_by_manager = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True, null=True)
    meeting_date = models.DateField(blank=True, null=True)
    meeting_time = models.TimeField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    log = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.applicant


class EmailLog(models.Model):
    applicant = models.CharField(max_length=255, null=True, blank=True)
    sender_name = models.CharField(max_length=255)
    to_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    logs = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.sender_name} to {self.to_email} - {self.subject}"