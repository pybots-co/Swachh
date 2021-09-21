 before_free_space = diskUsage()

    cleanup(job1)
    createBatScript(job2)
    cleanup(job1)

    after_free_space = diskUsage()

    total_cleaned_space = cleaned(before_free_space, after_free_space)
    total_cleaned_space = max(total_cleaned_space, 0)
    printCommand(heading="Total Disk space cleaned", description=str(total_cleaned_space) + "MB")

    checkSafetyOfPythonPackages()
    clean_site_packages(job3)

    user_renderables = [Panel(i, expand=True) for i in summary]
    progress_table.add_row(Panel.fit(Columns(user_renderables), title="Summary", border_style="cyan", padding=(1, 2)))