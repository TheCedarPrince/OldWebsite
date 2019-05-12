---
title: "Taming Knowledge - A Scholar's Guide to Managing Your Findings"
image:
  path: /assets/Taming Knowledge/library.jpg
  caption: "Photo from [@alfonsmc10](https://unsplash.com/@alfonsmc10)"
comments: true
share: true
---

*My workflow for capturing, storing, and sharing information from a personal knowledge base.*
{: .notice}
{: style="text-align: center;"}

&nbsp;

<figure class="align-center">
  <img src="{{ '/assets/Taming Knowledge/einstein.jpg' | absolute_url }}" alt="">
  <figcaption>Don't panic, yesterday's messy desk is today's web browser with 10+ tabs open.</figcaption>
</figure>

&nbsp;

<span class="dropcap" style="float: left; font-size: 55px; line-height: 1; margin-right: 5px; height: 50px;">A<span style="display: inline; height: 66px;"></span></span> common trend that I have found over the past few years while working alongside academics is that there is no easy way to capture, store, and share information relevant to projects or research - this being most bitter of ironies as ***science is built on collaboration.***

Over the past couple years, I have developed a method of capturing information, storing it alongside notes or annotations, and having it be shareable to others. **Outlined below is my method for building your own knowledge base workflow.**

&nbsp;
#  Knowledge Base Criteria
{: style="text-align: center;"}

### *I operate under the assumption that I may wake up one morning and that software or app is not supported anymore*
{: style="text-align: center;"}
{: .notice}


My personal criteria for a good knowledge base is that it must:

1. **Cost as little as possible** - whether you are a student or a professional, it is always great to save money where possible

2. **Be platform independent** - whether you are on OSX, Linux, Android, Windows, or iOS, you can access the materials across all these different platforms *easily*

3. **Has some redundancy and back-ups** - NOTHING is worse than having your computer, tablet, or phone die, break, or get stolen; having safety measures to provide back-ups is a must

4. **Allows for flexibility and creative solutions** - I never want to be tied down to any particular ecosystem because I operate under the assumption that I may wake up one morning and that software or app is not supported anymore

5. **Does it get the job done, easily?** - one can come up with a great solution, but if it takes you 30 minutes to process a paper into your workflow, that is not going to cut it



&nbsp;
# My Workflow
{: style="text-align: center;"}

**If you want to copy my workflow, go through each section individually starting with the first one - Cloud Storage.** Otherwise, my system is broken into three different parts as follows - feel free to click on each category to jump ahead:

**Cloud Storage** - the cloud is here to save the day!

**Reference Mangement** - organizing all those pdfs, papers, and articles

**Reading & Note Taking** - I always take notes on things I read - can't live without it!

&nbsp; 
# Cloud Storage
{: style="text-align: center;"}

<figure class="align-center">
  <img src="{{ '/assets/Taming Knowledge/cloud_storage.png' | absolute_url }}" alt="">
  <figcaption>To the sky - er, clouds I suppose.</figcaption>
</figure>

[Nextcloud](https://nextcloud.com), [Box](https://www.box.com), [Google Drive](https://www.google.com/intl/en/drive/), [Dropbox](https://www.dropbox.com/) - the list goes on and on about which cloud service you could use to meet your data management needs. 

With that said, narrowing down a specific cloud service can be tricky. However, for me, I ended up choosing Google Drive: it has a huge amount of storage that one can use for free - 15GB! - and integrates into my established work flow pretty well. 

**My biggest piece of advice is to look at what both supports you now and that you can see supporting you in the future.** I personally do not see filling up the 15GB soon and I know that I will not be storing exremely sensitive information on the service. 

In the future, I really want to move on to using [Nextcloud](https://nextcloud.com) as I like their model and you have more control over your data. For now, I do not want to worry terribly about what cloud architecture I have in place as **I know I can pretty easily swap out one cloud storage service for another should the need arise.**

&nbsp;
# Reference Management
{: style="text-align: center;"}

&nbsp;

<figure class="align-center">
  <img src="{{ '/assets/Taming Knowledge/zotero.png' | absolute_url }}" alt="">
  <figcaption>Zotero is the Hero!</figcaption>
</figure>

&nbsp;
### Why Zotero?
{: style="text-align: center;"}

After reviewing reference management tools like EndNote and Mendeley, I came to the conclusion that they are either

1. Too costly

2. Locks you into their app and software ecosystem

3. Not easy to share cross platform

Therefore, I came to the conclusion that **[Zotero](https://www.zotero.org) is the best reference manager out there that meets my requirements.** The process to get started with Zotero is pretty [straightforward](https://www.zotero.org/support/quick_start_guide) and there are a plethora of tutorials available on [YouTube](https://www.youtube.com/results?search_query=zotero+set-up) and the [Zotero documentation](https://www.zotero.org/support/) is extremely extensive!

What I like most about Zotero is its flexibility and that the entire code base is open source. There is a thriving community around Zotero that is actively developing it, creating extensions and lobbying new ideas - everything that I want to see in an open source software. :smiley:

&nbsp;
### Setting Up ZotFile
{: style="text-align: center;"}

Once you have followed one of the tutorials, I would suggest you install [Zotfile](http://zotfile.com) into Zotero. It can be a little tricky to configure so let me walk you through it.

_The following tutorial was heavily adapted from this [great guide](/assets/Taming Knowledge/zotfile_guide.pdf) written by Stephen Chignell. If anything is confusing, please consult this guide!_

1. Install [ZotFile](zotfile.com) from their website. This will download a .xpi file on your computer. 

2. Install ZotFile into Zotero by going to Tools and then select Add-ons. In the menu that shows up, click the gear icon and click "Install Add-on from File"

3. Select the .xpi you downloaded and install it.

4. Restart Zotero. 

Once you have finished installing ZotFile, now comes the more challenging part - configuring your cloud storage option for Zotero! 

1. Wherever you have your cloud storage set up on your computer, create a folder there named Zotero (or whatever you deem fit for your knowledge base).

2. Under the Tools menu, you should now see "ZotFile Preferences" as an option. Click that! 

&nbsp;

<figure class="align-center">
  <img src="{{ '/assets/Taming Knowledge/zotfile_preferences.png' | absolute_url }}" alt="">
</figure>

&nbsp;
{:start="3"}
3. The above screen - or something very similar to it - should appear. What is most important is that you go to the part that says "Location of Files" and change it to the path where you stored your Zotero folder in the first step. _Note: You can configure this section a lot more but for simplicity's sake, I'd suggest leaving everything like I have aside from the custom path. See the Stephen Chignell's guide for more info_

4. To make your Zotero database link to the cloud, go to "Zotero Preferences". Under the "Sync" page, uncheck the box next to "Sync attachment files in My Library" in the "File Syncing" category (see the photo below for help!).

&nbsp;

<figure class="align-center">
  <img src="{{ '/assets/Taming Knowledge/zotero_sync.png' | absolute_url }}" alt="">
</figure>

&nbsp;
### Testing Zotero
{: style="text-align: center;"}

Finally, let's test Zotero with ZotFile! 

1. Let's take one of my favorite papers [here](/assets/Taming Knowledge/npjschz201530.pdf) and download it. 

2. Once it is downloaded, drag the file into Zotero and watch the magic happen! What you should see is that ZotFile automatically extracted the metadata from the file and put the info into a Zotero reference. 

&nbsp;

<figure class="align-center">
  <img src="{{ '/assets/Taming Knowledge/zotfile_extraction.png' | absolute_url }}" alt="">
  <figcaption>Automatically grabs all the meta data from a file. This may fail occasionally on poorly formatted files!</figcaption>
</figure>

&nbsp;
{:start="3"}
3. **To get Zotero to save files to your specific cloud path, right click your recently uploaded file in Zotero and under "Manage Attachments", click "Rename Attachments".** Once done, you can now check your cloud service and you should see your PDF there! 

4. ZotFile also allows you to extract comments and annotations from a PDF that you upload or work on later in your Zotero Cloud set-up. To do this, right click a file that you have annotated and uploaded to Zotero. Under "Manage Attachments", click "Extract Annotations". Wait for a moment and you should see your annotations pop up under your entry in Zotero as a note file! 

&nbsp;

<figure class="align-center">
  <img src="{{ '/assets/Taming Knowledge/zotfile_annotations.png' | absolute_url }}" alt="">
  <figcaption>Zotero + ZotFile  :heart:</figcaption>
</figure>

&nbsp;
{% include disqus-comments.html %}

# Reading & Note Taking
{: style="text-align: center;"}

<figure class="align-center">
  <img src="{{ '/assets/Taming Knowledge/annotated_paper.png' | absolute_url }}" alt="">
  <figcaption>Nothing like some light reading! Now what to do with these notes?</figcaption>
</figure>

&nbsp;
### Don't Read a Paper - Devour It!
{: style="text-align: center;"}

**Pick a PDF reader on your desktop and mobile that allows you to do annotations, notes, screenshots, and comments. At least.** For me, I use [FoxIt Reader](https://www.foxitsoftware.com/pdf-reader/) because 1) Has a wide assortment of tools and is very easy to work with once you get the hang of it 2) has a mobile app for the iPhone 3)  it allows me to directly access my knowledge base on Google Drive either on the go or on desktop. This was the software that worked best for me - if something goes wrong, I know I can replace it but for now, it kicks butt! 

&nbsp;
### Enter Joplin - A Notetaker's Companion
{: style="text-align: center;"}

<figure class="align-center">
  <img src="{{ '/assets/Taming Knowledge/joplin.png' | absolute_url }}" alt="">
  <figcaption>What started out as a quest to write down an email turned into something awesome.</figcaption>
</figure>

When I first discovered Joplin I was stunned - it was PERFECT! It checked off all my boxes for what I can do:

1. Has cross platform support - mobile too! :heavy_check_mark:
2. Let's me make notes the way I want :heavy_check_mark:
3. Allows attachments of any kind :heavy_check_mark:
4. Organized note hierarchy :heavy_check_mark:
5. Active development team :heavy_check_mark:
6. It's Open Source :heavy_check_mark:
7. It's free :heavy_check_mark:

It sets itself up to be a competitor against the likes of EverNote and OneNote. Personally, I think this beats them. Read about Joplin [here](https://joplinapp.org) and give it a whirl! 

&nbsp;
# Concluding Thoughts
{: style="text-align: center;"}

As I mentioned earlier, **"I operate under the assumption that I may wake up one morning and that software or app is not supported anymore."** I tried to leave most of my recommendations here pretty general so that way you could have the flexibility to do what you wanted. I only firmly recommended Joplin and Zotero due to the fact that I personally think they are wonderful tools that can serve my purposes - **if you have a better workflow or other ideas, please let me know in the comments below!**

Keep on and rock on. ![zelko](/assets/favicon.ico)

-----
![left-aligned-image](/assets/150x_profile.png){: .align-left} <br> Jacob S. Zelko is a senior at Georgia Institute of Technology studying Biomedical Engineering and doing research in areas of computational psychiatry and medical surveillance. When not working, Jacob can be found writing music, reading, or drinking hot cocoa at random coffee houses. :coffee:

-----