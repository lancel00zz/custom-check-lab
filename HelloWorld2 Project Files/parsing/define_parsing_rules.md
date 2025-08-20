autoFilledRule1 %{date("yyyy-MM-dd HH:mm:ss,SSS"):date} %{notSpace:level}: %{notSpace:emoji} File count changed: %{integer:file_count.old} → %{integer:file_count.new} on %{notSpace:server}
